from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (CHAIN, DIRECT, FILLER, PART, RIGHT_C, WRONG_C, bit_row, chip, load, mark,
                                   seeds_plot)

MODE_C = {"direct": DIRECT, "filler": FILLER, "chain": CHAIN}


def verdict(a: float) -> str:
    return "solved" if a > 0.95 else "shaky" if a > 0.65 else "a coin flip"


class Chain(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.depth()
        self.theory()
        self.filler()
        self.results()
        self.replay()

    def card(self):
        card = chapter_card(1, r"Thinking out loud is computing", r"Why does writing the steps help?",
                            lit=(2022, 2024), part=PART)
        with self.voiceover("Chapter one. Thinking out loud is computing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def puzzle(self):
        p = load("parity")
        d16, c16 = p["accs_direct16"], p["accs_chain16"]
        bits = np.random.default_rng(17).integers(0, 2, 16)
        run = np.cumsum(bits) % 2
        row = bit_row(bits, size=0.5, buff=0.1).move_to(UP * 1.9)
        q = label(r"Is the number of $1$s odd?", font_size=34).next_to(row, UP, buff=0.4)
        stack = VGroup(*[RoundedRectangle(width=2.6, height=0.5, corner_radius=0.1, stroke_color=DIRECT, stroke_width=2,
                                          fill_color=DIRECT, fill_opacity=0.12) for _ in range(2)]).arrange(UP, buff=0.12)
        stack.move_to([-2.2, -0.6, 0])
        st = label(r"$2$ layers, \\ then answer", font_size=22, color=DIRECT).next_to(stack, LEFT, buff=0.25)
        feeds = VGroup(*[Line(b.get_bottom(), stack.get_top(), stroke_width=1.2, color=DIRECT).set_stroke(opacity=0.35)
                         for b in row])
        out1 = chip("?", size=0.55, color=DIRECT).next_to(stack, DOWN, buff=0.45)
        a1 = Arrow(stack.get_bottom(), out1.get_top(), buff=0.06, stroke_width=3, color=DIRECT,
                   max_tip_length_to_length_ratio=0.3)
        r1 = label(rf"right ${100 * np.mean(d16):.0f}\%$ of the time", font_size=28, color=DIRECT)
        r1.next_to(out1, DOWN, buff=0.3)
        par = VGroup(*[chip(str(int(v)), size=0.5, color=CHAIN) for v in run])
        for c_, b in zip(par, row):
            c_.move_to(b.get_center() + DOWN * 0.95)
        pl = label(r"odd so far?", font_size=22, color=CHAIN).next_to(par, LEFT, buff=0.25)
        ring = SurroundingRectangle(VGroup(row[0], par[0]), color=C.BITS, buff=0.08, stroke_width=3, corner_radius=0.08)
        r2 = label(rf"writing its work first: \ right ${100 * np.mean(c16):.0f}\%$", font_size=28, color=CHAIN)
        r2.move_to([2.6, -1.9, 0])
        ans = SurroundingRectangle(par[-1], color=CHAIN, buff=0.06, stroke_width=4)
        tag = note(rf"one string shown; \ accuracy on $1{{,}}000$ new strings, \ mean of ${len(d16)}$ training runs")
        tag.to_corner(DR, buff=0.25)
        coin = "a coin flip" if np.mean(d16) < 0.6 else "far from reliable"
        with self.voiceover(
            "Here's a puzzle for a small transformer: sixteen bits. Is the number of ones odd? "
            "<bookmark mark='a'/> Trained to answer straight away, our two-layer model is right "
            f"{100 * np.mean(d16):.0f} percent of the time: {coin}. <bookmark mark='b'/> Now train the very same "
            "model to write its work first: going along the bits, is the count odd so far? Each step is easy, just "
            f"the last answer and one more bit. <bookmark mark='c'/> Its final answer is right "
            f"{100 * np.mean(c16):.0f} percent of the time. Same model, same size. It just got to think out loud."
        ) as vo:
            self.play(FadeIn(q), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in row], lag_ratio=0.05), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(stack), FadeIn(st), LaggedStart(*[Create(f) for f in feeds], lag_ratio=0.03), run_time=1.2)
            self.play(GrowArrow(a1), FadeIn(out1))
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(stack, st, feeds, a1, out1)), r1.animate.scale(0.8).move_to([-3.6, -1.9, 0]))
            self.play(Create(ring), FadeIn(pl))
            for i in range(len(par)):
                if i:
                    self.play(ring.animate.move_to(VGroup(row[i], par[i])), run_time=0.12)
                self.play(FadeIn(par[i], shift=DOWN * 0.1), run_time=0.12)
            self.play(FadeOut(ring))
            vo.wait_until("c")
            self.play(Create(ans), FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        L, P, W = 4, 5, 6  # layers, prompt tokens, tokens written
        T = P + W
        dx, dy = 1.0, 0.72
        x0, y0 = -5.4, -1.9

        def at(l, t):
            return np.array([x0 + t * dx, y0 + l * dy, 0])

        nodes = VGroup(*[Dot(at(l, t), radius=0.07, color=GREY_B if t < P else CHAIN).set_opacity(0.9 if l else 0.6)
                         for t in range(T) for l in range(L + 1)])
        ups = VGroup(*[Line(at(l, t), at(l + 1, t), stroke_width=1.5, color=GREY_D) for t in range(T) for l in range(L)])
        att = VGroup(*[Line(at(l, s), at(l + 1, t), stroke_width=0.8, color=GREY_D).set_stroke(opacity=0.45)
                       for t in range(T) for s in range(max(0, t - 2), t) for l in range(L)])
        toks = VGroup(*[label(r"$x_{%d}$" % (t + 1), font_size=20, color=GREY_B if t < P else CHAIN)
                        .next_to(at(0, t), DOWN, buff=0.15) for t in range(T)])
        ll = VGroup(*[label(rf"layer ${l}$", font_size=18, color=GREY_C).next_to(at(l, 0), LEFT, buff=0.25)
                      for l in range(1, L + 1)])
        back = VGroup(*[CurvedArrow(at(L, t) + UR * 0.06, at(0, t + 1) + LEFT * 0.12, angle=-PI / 3, stroke_width=2,
                                    color=CHAIN, tip_length=0.12) for t in range(P - 1, T - 1)])
        bl = label(r"each written token goes back in", font_size=22, color=CHAIN).next_to(at(L, P + 2), UP, buff=0.35)
        one = [at(0, 0)] + [at(l, min(l, P - 1)) for l in range(1, L + 1)]
        one[-1] = at(L, P - 1)
        p1 = VMobject(stroke_width=6, color=DIRECT).set_points_as_corners(one)
        snake = [at(0, P - 1)]
        for t in range(P - 1, T):
            snake += [at(L, t)]
            if t < T - 1:
                snake += [at(0, t + 1)]
        p2 = VMobject(stroke_width=6, color=C.BITS).set_points_as_corners(snake)
        colors = {r"L": GREY_A, r"k": CHAIN}
        f1 = cmath(r"\text{at once:}\quad", r"L", r"\text{ steps in a row}", colors=colors, font_size=30)
        f2 = cmath(r"\text{with } ", r"k", r"\text{ tokens of thought:}\quad", r"L", r"\,(k+1)", colors=colors,
                   font_size=30)
        VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.35).shift(RIGHT * 1.0)
        tag = note(r"schematic: \ $4$ layers").to_corner(DL, buff=0.25)
        with self.voiceover(
            "Why does writing help? Look at the computation. A transformer runs every token through the same fixed "
            "stack of layers. <bookmark mark='a'/> Answering at once, the longest chain of steps that happen one "
            "after another is as tall as the stack: L layers, however hard the question. <bookmark mark='b'/> But a "
            "token it writes goes back in as input. <bookmark mark='c'/> So the chain of steps can climb the stack, "
            "come back down, and climb again, once per token. With k tokens of thought, L times k plus one steps in a "
            "row. The written tokens are a scratchpad, and a clock: each one buys another pass through the network."
        ) as vo:
            self.play(FadeIn(nodes[: (L + 1) * P]), FadeIn(toks[:P]), FadeIn(ll), FadeIn(tag),
                      Create(VGroup(*[u for u in ups if u.get_start()[0] < x0 + P * dx - 0.5])),
                      Create(VGroup(*[a for a in att if a.get_end()[0] < x0 + P * dx - 0.5])), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(p1), Write(f1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(nodes[(L + 1) * P:]), FadeIn(toks[P:]),
                      FadeIn(VGroup(*[u for u in ups if u.get_start()[0] > x0 + P * dx - 0.5])),
                      FadeIn(VGroup(*[a for a in att if a.get_end()[0] > x0 + P * dx - 0.5])),
                      LaggedStart(*[Create(b) for b in back], lag_ratio=0.2), FadeIn(bl), run_time=2.0)
            vo.wait_until("c")
            dot = glow_dot(snake[0], color=C.BITS, radius=0.09)
            self.play(p1.animate.set_stroke(opacity=0.3), FadeIn(dot))
            self.play(Create(p2), MoveAlongPath(dot, p2.copy()), Write(f2), run_time=4.0, rate_func=linear)
            self.play(Circumscribe(f2, color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theory(self):
        t1 = theorem_card(r"no chain", r"a transformer of fixed depth, \ its numbers kept to $O(\log n)$ bits, \ "
                          r"computes only what constant-depth threshold circuits compute: \ the class TC$^0$",
                          who=r"W.~Merrill \& A.~Sabharwal (2023)", width=6.6, font_size=21, color=DIRECT)
        t2 = theorem_card(r"a chain of $T$ steps", r"a transformer of constant depth that writes $T$ tokens can "
                          r"simulate any Boolean circuit of size $T$; \ with polynomially many, \ it decides exactly "
                          r"the problems solvable in polynomial time, P",
                          who=r"Z.~Li, H.~Liu, D.~Zhou \& T.~Ma (2024); \ Merrill \& Sabharwal (2024)", width=6.6,
                          font_size=21, color=CHAIN)
        VGroup(t1, t2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.25, 0.15, 0])
        # nested classes, each with a problem that lives at its edge
        cx = 3.6
        sets, labs = VGroup(), VGroup()
        for k, (name, w, h, col) in enumerate(((r"P", 6.4, 6.0, CHAIN), (r"NC$^1$", 5.0, 4.4, GREY_B),
                                               (r"TC$^0$", 3.6, 2.9, DIRECT), (r"AC$^0$", 2.0, 1.3, GREY_C))):
            e = Ellipse(width=w, height=h, stroke_color=col, stroke_width=2.5).move_to([cx, -0.1 - (6.0 - h) * 0.32, 0])
            sets.add(e)
            labs.add(label(name, font_size=24, color=col).move_to(e.get_top() + DOWN * 0.3))
        ex = VGroup(
            label(r"parity", font_size=20, color=DIRECT).move_to(sets[2].get_top() + DOWN * 0.95),
            label(r"composing permutations \\ of five objects", font_size=18, color=GREY_A)
            .move_to(sets[1].get_top() + DOWN * 0.75),
            label(r"evaluating a circuit", font_size=18, color=CHAIN).move_to(sets[0].get_top() + DOWN * 0.7),
        )
        sch = note(r"schematic: \ believed strict, \ not all proved").next_to(sets, DOWN, buff=0.12)
        keep_in_frame(sch)
        honest = label(r"parity is in TC$^0$: \ a fixed depth can compute it in principle. \\ What failed above is "
                       r"learning it: \ every bit flips the answer", font_size=22, color=GREY_A)
        honest.to_corner(DL, buff=0.35)
        cite_ = cite(r"Furst, Saxe \& Sipser (1984); \ Barrington (1989); \ Hahn (2020); \ Feng et al.\ (2023)",
                     corner=UL)
        with self.voiceover(
            "Theory makes this precise. <bookmark mark='a'/> In 2023 William Merrill and Ashish Sabharwal showed "
            "that a transformer of fixed depth, answering at once, computes only what circuits of constant depth "
            "with threshold gates can compute, a class called TC zero. <bookmark mark='b'/> Problems believed to lie "
            "outside it need depth that grows with the input: composing a long list of permutations of five objects "
            "is the classic one. <bookmark mark='c'/> A chain of thought lifts the limit. With T tokens of thought, a "
            "constant-depth transformer can simulate any circuit of size T; with polynomially many, it decides "
            "exactly the problems a computer can solve in polynomial time. <bookmark mark='d'/> One honest caveat: "
            "parity itself is inside TC zero. A fixed-depth network can compute it in principle; what failed in our "
            "experiment is learning it, because every single bit flips the answer."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(t1, shift=UP * 0.15), Create(sets[2]), FadeIn(labs[2]), Create(sets[3]), FadeIn(labs[3]))
            vo.wait_until("b")
            self.play(Create(sets[1]), FadeIn(labs[1]), FadeIn(ex[1]), FadeIn(sch))
            vo.wait_until("c")
            self.play(FadeIn(t2, shift=UP * 0.15), Create(sets[0]), FadeIn(labs[0]), FadeIn(ex[2]))
            vo.wait_until("d")
            self.play(FadeIn(ex[0]), Indicate(ex[0], color=DIRECT), FadeIn(honest))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def filler(self):
        p = load("parity")
        bits = np.random.default_rng(17).integers(0, 2, 8)
        run = np.cumsum(bits) % 2

        def row_of(kind):
            g = VGroup(*[chip(str(int(b)), 0.42, GREY_B, 22) for b in bits], chip("=", 0.42, GREY_C, 22, fill=0))
            if kind == "filler":
                g.add(*[chip(".", 0.42, FILLER, 22) for _ in bits], chip("?", 0.42, FILLER, 22))
            elif kind == "chain":
                g.add(*[chip(str(int(v)), 0.42, CHAIN, 22) for v in run])
            else:
                g.add(chip("?", 0.42, DIRECT, 22))
            return g.arrange(RIGHT, buff=0.06)

        rows = VGroup(row_of("direct"), row_of("filler"), row_of("chain")).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rows.move_to([0.9, 0.9, 0])
        names = VGroup(*[label(t, font_size=22, color=c).next_to(r, LEFT, buff=0.35) for t, c, r in
                         ((r"answer at once", DIRECT, rows[0]), (r"$n$ dots, then answer", FILLER, rows[1]),
                          (r"the running parity", CHAIN, rows[2]))])
        acc = {m: p[f"accs_{m}16"] for m in ("direct", "filler", "chain")}
        res = VGroup(*[label(rf"${100 * np.mean(acc[m]):.0f}\%$", font_size=30, color=MODE_C[m]) for m in acc])
        for r_, row in zip(res, rows):
            r_.move_to([6.2, row.get_y(), 0])
        rh = label(r"right, \ $16$ bits", font_size=20, color=GREY_A).next_to(res, UP, buff=0.3)
        why_ = label(r"a dot is input, \ not output: \ more positions to compute in, \\ but no extra step in a row",
                     font_size=24, color=FILLER).move_to([0, -2.0, 0])
        cite_ = cite(r"J.~Pfau, W.~Merrill \& S.~Bowman, \textit{Let's Think Dot by Dot} (2024)", corner=DL)
        fd, dd, cd = np.mean(acc["filler"]), np.mean(acc["direct"]), np.mean(acc["chain"])
        if fd < dd + 0.1:
            said_ = (f"the dots don't help: {100 * fd:.0f} percent, no better than answering at once. Each dot is "
                     "input, not output; it adds positions to compute in, but nothing flows from the top of one "
                     "position to the bottom of the next. It is the written steps, not the extra length, that do the "
                     "work.")
        else:
            said_ = (f"the dots help a little, {100 * fd:.0f} percent against {100 * dd:.0f}: more positions give "
                     "more parallel computation. But nothing flows from the top of one position to the bottom of the "
                     f"next, and the written chain, at {100 * cd:.0f}, is in another league.")
        with self.voiceover(
            "Is it the extra tokens, or what's in them? Give the model the same number of extra positions, filled "
            "with meaningless dots, and train it to answer after them. <bookmark mark='a'/> On sixteen bits, "
            + said_ + " <bookmark mark='b'/> Jacob Pfau, Merrill and Sam Bowman showed in 2024 that dots can help on "
            "problems that split into independent parallel pieces, and that a model needs dense supervision to learn "
            "to use them."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(n_, r_)) for n_, r_ in zip(names, rows)], lag_ratio=0.4),
                      FadeIn(rh), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, scale=1.3) for r_ in res], lag_ratio=0.3), FadeIn(why_))
            vo.wait_until("b")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        p = load("parity")
        ns = [int(n) for n in p["ns"]]
        modes = ("direct", "filler", "chain")
        g = axes([0, 3], [0, 1], x_length=7.4, y_length=3.8, ylabel=r"right on $1{,}000$ new strings",
                 yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-1.4, -0.2, 0])
        ax = g.ax
        chance = DashedLine(ax.c2p(0, 0.5), ax.c2p(3, 0.5), color=GREY_D, stroke_width=1.5)
        cl = label(r"chance", font_size=18, color=GREY_C).next_to(ax.c2p(3, 0.5), RIGHT, buff=0.08)
        bw = 0.42
        bars = {m: VGroup() for m in modes}
        whisk = VGroup()
        for i, n in enumerate(ns):
            for j, m in enumerate(modes):
                vals = p[f"accs_{m}{n}"]
                v = float(np.mean(vals))
                x = ax.c2p(i + 0.5, 0)[0] + (j - 1) * bw * 1.15
                b = Rectangle(width=bw, height=max(ax.y_length * v, 0.01), stroke_width=0, fill_color=MODE_C[m],
                              fill_opacity=0.85).move_to([x, ax.c2p(0, 0)[1], 0], aligned_edge=DOWN)
                bars[m].add(b)
                if len(vals) > 1:
                    lo, hi = ax.c2p(0, min(vals))[1], ax.c2p(0, max(vals))[1]
                    whisk.add(Line([x, lo, 0], [x, hi, 0], color=WHITE, stroke_width=2))
        xt = VGroup(*[label(rf"$n = {n}$ bits", font_size=22, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
                      for i, n in enumerate(ns)])
        key = legend([(DIRECT, r"answer at once"), (FILLER, r"$n$ dots, then answer"), (CHAIN, r"the running parity "
                                                                                             r"first")], font_size=20)
        key.next_to(g, RIGHT, buff=0.4).shift(UP * 0.6)
        wl = note(rf"$16$ bits: \ mean of ${int(p['seeds'])}$ runs, \\ line: \ lowest to highest", font_size=18)
        wl.next_to(key, DOWN, buff=0.9).align_to(key, LEFT)
        d = [float(np.mean(p[f"accs_direct{n}"])) for n in ns]
        c = [float(np.mean(p[f"accs_chain{n}"])) for n in ns]
        with self.voiceover(
            "Here are all our runs, on strings of four, eight and sixteen bits. <bookmark mark='a'/> Answering at "
            f"once is {verdict(d[0])} at four bits, {verdict(d[1])} at eight, and {verdict(d[2])} at sixteen. "
            "<bookmark mark='b'/> The dots follow it down. <bookmark mark='c'/> With the running parity written "
            f"first, all three are {'solved' if min(c) > 0.95 else 'much better'}, in every run."
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(cl), FadeIn(xt))
            for k, m in zip("abc", modes):
                vo.wait_until(k)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[m]], lag_ratio=0.3), FadeIn(key[modes.index(m)]))
            self.play(FadeIn(whisk), FadeIn(wl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        """Training at 16 bits, replayed: the curves scrubbed together with the chain the model writes."""
        p = load("parity")
        S = int(p["seeds"])
        Cc = np.stack([np.asarray(p[f"curve_chain_{s}"]) for s in range(S)])
        Cd = np.stack([np.asarray(p[f"curve_direct_{s}"]) for s in range(S)])
        steps = Cc[0, :, 0]
        smax = float(steps[-1])
        g = axes([0, smax], [0.3, 1.0], x_length=5.6, y_length=3.4, xlabel=r"training steps",
                 ylabel=r"right on new strings, \ $16$ bits", xticks=[0, smax / 2, smax],
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yticks=[0.5, 1.0],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-3.6, -0.6, 0])
        ax = g.ax
        kt = ValueTracker(0)
        Yc, Yd = np.clip(Cc[:, :, 1], 0.3, 1), np.clip(Cd[:, :, 1], 0.3, 1)

        def partial(Y, col):
            i = int(round(kt.get_value()))
            return seeds_plot(ax, steps[:i + 1], Y[:, :i + 1], col) if i >= 1 else VGroup()

        lc = always_redraw(lambda: partial(Yc, CHAIN))
        ld = always_redraw(lambda: partial(Yd, DIRECT))
        R = np.asarray(p["replay_chain"])  # (checkpoints, strings, 16): the chain it writes
        probe = np.asarray(p["probe"])  # (strings, 16)
        truth = np.cumsum(probe, 1) % 2
        n = probe.shape[1]
        sz = 0.3
        inputs = VGroup()
        for s in range(len(probe)):
            inputs.add(VGroup(*[chip(str(int(b)), sz, GREY_B, 14) for b in probe[s]]).arrange(RIGHT, buff=0.04))
        inputs.arrange(DOWN, buff=0.62).move_to([3.4, 0.55, 0])

        def chain_at(k):
            g_ = VGroup()
            for s in range(len(probe)):
                r_ = VGroup(*[chip(str(int(v)), sz, RIGHT_C if v == t else WRONG_C, 14, fill=0.3)
                              for v, t in zip(R[k, s], truth[s])]).arrange(RIGHT, buff=0.04)
                r_.next_to(inputs[s], DOWN, buff=0.08)
                g_.add(r_)
            return g_

        il = label(r"three strings, \ and the chain it writes", font_size=22, color=CHAIN).next_to(inputs, UP, buff=0.3)
        key = VGroup(label(r"green: \ the true running parity", font_size=18, color=RIGHT_C),
                     label(r"red: \ a wrong step", font_size=18, color=WRONG_C)).arrange(RIGHT, buff=0.4)
        key.next_to(VGroup(inputs, chain_at(0)), DOWN, buff=0.3)
        lg = legend([(CHAIN, r"chain"), (DIRECT, r"at once")], font_size=18).next_to(ax, UP, buff=0.05)
        lg.align_to(ax, RIGHT)
        tag = note(rf"computed: \ ${S}$ runs each, \ band: lowest to highest; \ chains from run $1$").to_corner(DR, buff=0.2)
        mk = always_redraw(lambda: Line(ax.c2p(steps[int(round(kt.get_value()))], 0.3),
                                        ax.c2p(steps[int(round(kt.get_value()))], 1.0), color=C.BITS, stroke_width=3))
        k_hit = [int(k) for k in range(len(steps)) if (R[k] == truth).all()]
        first = int(steps[k_hit[0]]) if k_hit else None
        cur = chain_at(0)
        dfin = float(Yd[:, -1].mean())
        if first:
            grow = (f"Then it learns the first few steps, and the right stretch grows along the string, one position "
                    f"after another: by step {first:,} all three chains are right.")
        else:
            grow = "Then it learns the first few steps, and the right stretch grows along the string."
        if dfin < 0.6:
            floor = "Answering at once never gets off the floor."
        else:
            floor = f"Answering at once ends at {100 * dfin:.0f} percent."
        with self.voiceover(
            "Here is the training at sixteen bits, replayed. On the left, accuracy as each model trains, three runs "
            "of each. On the right, the chain the model writes for three strings, checked bit by bit. "
            f"<bookmark mark='a'/> At first the chain is noise. <bookmark mark='b'/> {grow} <bookmark mark='c'/> "
            f"{floor} The chain is not just more powerful; it is easier to learn, because each step is a small, "
            "local problem."
        ) as vo:
            self.play(FadeIn(g), FadeIn(inputs), FadeIn(il), FadeIn(key), FadeIn(lg), FadeIn(tag), FadeIn(cur))
            self.add(lc, ld)
            vo.wait_until("a")
            self.add(mk)
            vo.wait_until("b")
            K = len(steps)
            dt = max(0.25, min(0.6, (vo.until("c") - 0.5) / K))
            for k in range(1, K):
                self.play(Transform(cur, chain_at(k)), kt.animate.set_value(k), run_time=dt, rate_func=linear)
            vo.wait_until("c")
            self.play(Indicate(lg[1], color=DIRECT))
        for m in (lc, ld, mk):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
