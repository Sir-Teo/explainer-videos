from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, LAZY, PART, RICH, SP, load, predict_card, takeaway_card

TR, TE = GREY_B, C.BITS


class Grok(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.curves()
        self.predict()
        self.decay()
        self.fourier()
        self.circuit()
        self.takeaway()

    def card(self):
        card = chapter_card(15, r"Grokking", r"Can understanding arrive long after memorizing?", lit=(2022,), part=PART)
        with self.voiceover("Chapter fifteen. Grokking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def task(self):
        g = load("grok")
        P = int(g["P"])
        n = 24  # a corner of the table, drawn
        cells = VGroup()
        rg = np.random.default_rng(0)
        shown = rg.random((n, n)) < 0.4
        for a in range(n):
            for b in range(n):
                sq = Square(0.2, stroke_width=0.6, stroke_color=GREY_D,
                            fill_color=C.TRUE_P if shown[a, b] else BACKGROUND, fill_opacity=0.6 if shown[a, b] else 0)
                sq.move_to([-6.0 + 0.2 * b, 2.4 - 0.2 * a, 0])
                cells.add(sq)
        tl = label(rf"$(a + b) \bmod {P}$: \ a ${P} \times {P}$ table \ (a corner shown, \ illustrative)", font_size=22,
                   color=GREY_A)
        tl.next_to(cells, DOWN, buff=0.2).align_to(cells, LEFT)
        ex = VGroup(MathTex(rf"50 + 60 \equiv 13 \pmod{{{P}}}", font_size=40),
                    label(rf"clock arithmetic, \ on a clock with ${P}$ hours", font_size=26, color=GREY_A))
        ex.arrange(DOWN, buff=0.25).move_to([3.4, 1.6, 0])
        sh = label(rf"the network sees ${int(g['n_train']):,}$ entries ($40\%$) \\ and must fill in the other "
                   rf"${int(g['n_test']):,}$".replace(",", "{,}"), font_size=26, color=C.TRUE_P).next_to(ex, DOWN, buff=0.5)
        net = label(rf"each number a learned vector of ${int(g['dim'])}$; \ ${int(g['hid'])}$ ReLU units; \ a score "
                    r"per "
                    r"answer", font_size=22, color=GREY_A).next_to(sh, DOWN, buff=0.4)
        cite_ = cite(r"A.~Power, Y.~Burda, H.~Edwards, I.~Babuschkin \& V.~Misra, \textit{Grokking} (2022)", corner=DR)
        assert (50 + 60) % P == 13
        # the clock: P hours; 50, then 60 more, lands on 13
        cc, R_ = np.array([-3.6, 0.3, 0]), 1.7

        def at(k, r=R_):
            th = PI / 2 - TAU * k / P
            return cc + r * np.array([math.cos(th), math.sin(th), 0])

        dial = Circle(radius=R_, stroke_color=GREY_C, stroke_width=2).move_to(cc)
        ticks = VGroup(*[Line(at(k, R_ - (0.16 if k % 10 == 0 else 0.07)), at(k), stroke_width=1.2, color=GREY_B)
                         for k in range(P)])
        hands = VGroup(
            Arc(radius=R_ + 0.18, start_angle=PI / 2, angle=-TAU * 50 / P, arc_center=cc, stroke_color=C.BITS, stroke_width=5),
            Arc(radius=R_ + 0.32, start_angle=PI / 2 - TAU * 50 / P, angle=-TAU * 60 / P, arc_center=cc,
                stroke_color=C.TRUE_P, stroke_width=5))
        nums = VGroup(*[VGroup(Dot(at(k), radius=0.06, color=col), MathTex(str(k), font_size=26, color=col).move_to(at(k, R_ - 0.42)))
                        for k, col in ((0, GREY_A), (50, C.BITS), (13, C.TRUE_P))])
        clock = VGroup(dial, ticks, hands, nums)
        with self.voiceover(
            "In 2022, a team at OpenAI noticed something strange. Take a tiny task: addition on a clock with "
            f"{P} hours, so fifty plus sixty is thirteen. <bookmark mark='a'/> Show a small network forty percent of "
            "the addition table, and ask it to fill in the rest."
        ) as vo:
            self.play(Write(ex[0]), FadeIn(ex[1]), FadeIn(cite_), Create(dial), FadeIn(ticks), FadeIn(nums[0]))
            self.play(Create(hands[0]), FadeIn(nums[1]), run_time=1.2)
            self.play(Create(hands[1]), FadeIn(nums[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(clock))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.0008), FadeIn(tl), FadeIn(sh), FadeIn(net),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        g = load("grok")
        W, N = np.asarray(g["wd"]), np.asarray(g["nowd"])
        t_tr, t_te = int(g["t_train_wd"]), int(g["t_test_wd"])
        xmax = math.log10(max(W[-1, 0], N[-1, 0]))
        ax = Axes(x_range=[0, xmax + 0.1, 1], y_range=[0, 1, 0.25], x_length=8.2, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.5, -0.4, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3)) if v <= xmax + 0.1])
        yl = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1)])
        xn = label(r"training steps \ (log scale)", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)

        def lines(D, sw=3.5):
            lx = np.log10(D[:, 0])
            return curve(ax, lx, D[:, 1], TR, sw), curve(ax, lx, D[:, 2], TE, sw)

        ntr, _ = lines(N, 2.5)
        ntr.set_stroke(opacity=0.6)
        nte = DashedVMobject(curve(ax, np.log10(N[:, 0]), N[:, 2], C.SURPRISE, 4), num_dashes=90)
        key = VGroup(label(r"the $40\%$ it has seen", font_size=26, color=TR), label(r"the $60\%$ it hasn't", font_size=26, color=TE))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.8, 0])
        m1 = DashedLine(ax.c2p(math.log10(max(t_tr, 1)), 0), ax.c2p(math.log10(max(t_tr, 1)), 1), color=TR, stroke_width=2)
        m2 = DashedLine(ax.c2p(math.log10(t_te), 0), ax.c2p(math.log10(t_te), 1), color=TE, stroke_width=2)
        lag = label(rf"memorized by step ${t_tr:,}$; \\ generalized by step ${t_te:,}$".replace(",", "{,}"), font_size=26,
                    color=WHITE).next_to(key, DOWN, buff=0.45).align_to(key, LEFT)
        nowd = label(r"without weight decay (dashed): \\ not generalized by the run's end" if g["t_test_nowd"] is None else
                     rf"without weight decay (dashed): \\ much later, \ step ${int(g['t_test_nowd']):,}$".replace(",", "{,}"),
                     font_size=24, color=C.SURPRISE).next_to(lag, DOWN, buff=0.35).align_to(key, LEFT)
        lt = ValueTracker(0.0)
        lxw = np.log10(W[:, 0])

        def upto(k, col):
            n_ = max(2, int(np.searchsorted(lxw, lt.get_value(), side="right")))
            return curve(ax, lxw[:n_], W[:n_, k], col, 3.5)

        def acc(k):
            return 100 * float(np.interp(lt.get_value(), lxw, W[:, k]))

        live = [always_redraw(lambda: upto(1, TR)), always_redraw(lambda: upto(2, TE))]
        nums = always_redraw(lambda: VGroup(
            MathTex(rf"{acc(1):.0f}\%", font_size=26, color=TR).next_to(key[0], RIGHT, buff=0.25),
            MathTex(rf"{acc(2):.0f}\%", font_size=26, color=TE).next_to(key[1], RIGHT, buff=0.25)))
        clk = always_redraw(lambda: MathTex(rf"\text{{step }}{int(round(10 ** lt.get_value())):,}".replace(",", "{,}"),
                                            font_size=28, color=WHITE).next_to(ax.c2p(0, 1), UR, buff=0.15).shift(RIGHT * 0.2))
        wn = np.concatenate([W[:, 3], N[:, 3]])
        wax = CornerAxes(x_range=[0, xmax + 0.1, 1], y_range=[0, float(np.ceil(wn.max() / 20) * 20), 20], x_length=2.9,
                         y_length=1.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        shrinks, grows = W[-1, 3] < W[np.argmax(W[:, 3]), 3] * 0.8, N[-1, 3] > N[0, 3]
        wcap = label(r"the size of all the weights", font_size=20, color=GREY_A)
        wl1 = label(r"with weight decay: \ shrinks" if shrinks else r"with weight decay", font_size=18, color=TE)
        wl2 = label(r"without: \ grows" if grows else r"without", font_size=18, color=C.SURPRISE)
        winset = VGroup(wcap, wax, VGroup(wl1, wl2).arrange(DOWN, aligned_edge=LEFT, buff=0.06)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        winset.next_to(nowd, DOWN, buff=0.3).align_to(key, LEFT)
        keep_in_frame(winset, margin=0.2)
        wlines = VGroup(curve(wax, np.log10(W[:, 0]), W[:, 3], TE, 3),
                        DashedVMobject(curve(wax, np.log10(N[:, 0]), N[:, 3], C.SURPRISE, 3), num_dashes=40))
        ratio = t_te / max(t_tr, 1)
        said1 = (
            "Without weight decay, the same network does not get there within this run. " if g["t_test_nowd"] is None else
            f"Without weight decay, it takes until step {int(g['t_test_nowd']):,}. "
        )
        with self.voiceover(
            f"It memorizes the entries it was shown within about {t_tr:,} steps, and for a long time it gets the "
            "unseen ones no better than chance. <bookmark mark='a'/> Keep training anyway. "
            f"{ratio:.0f} times as long, at step {t_te:,}, accuracy on the unseen entries shoots up to nearly a "
            "hundred percent. The network has found the rule. They called it grokking. <bookmark mark='b'/> "
            + said1
            + "Weight decay keeps squeezing the weights, and a lookup table of memorized answers costs more weight "
            "than the rule."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(key))
            self.add(*live, nums, clk)
            self.play(lt.animate.set_value(math.log10(max(t_tr, 2)) + 0.6), run_time=3.5, rate_func=linear)
            self.play(Create(m1))
            vo.wait_until("a")
            self.play(lt.animate.set_value(float(lxw[-1])), run_time=4.0, rate_func=linear)
            for m_ in (*live, nums, clk):
                m_.clear_updaters()
            self.play(Create(m2), FadeIn(lag))
            vo.wait_until("b")
            self.play(Create(ntr), Create(nte), FadeIn(nowd), run_time=2.0)
            self.play(FadeIn(winset), Create(wlines), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        g = load("grok")
        wds = [float(v) for v in g["wds"]]
        st, sm = np.asarray(g["sweep_test"], float), np.asarray(g["sweep_train"], float)
        cap = int(g["max_steps"])
        xs = np.arange(len(wds))
        ax = CornerAxes(x_range=[-0.5, len(wds) - 0.5, 1], y_range=[1, math.log10(cap) + 0.4, 1], x_length=7.0, y_length=4.0,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-2.2, -0.5, 0])
        xt = VGroup(*[MathTex(f"{w:g}", font_size=24, color=GREY_B).next_to(ax.c2p(i, 1), DOWN, buff=0.1) for i, w in enumerate(wds)])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(-0.5, v), LEFT, buff=0.08)
                      for t, v in (("10", 1), ("100", 2), ("1{,}000", 3)) if v <= math.log10(cap) + 0.4])
        xn = label(r"weight decay", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"steps until \ (three seeds)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        capl = DashedLine(ax.c2p(-0.5, math.log10(cap)), ax.c2p(len(wds) - 0.5, math.log10(cap)), color=GREY_D, stroke_width=1.5)
        capt = label(rf"the run's end, \ step ${cap:,}$".replace(",", "{,}"), font_size=18, color=GREY_B)
        capt.next_to(ax.c2p(len(wds) - 0.5, math.log10(cap)), UL, buff=0.05)
        mem, gen, never = VGroup(), VGroup(), VGroup()
        for i in range(len(wds)):
            for k in range(st.shape[1]):
                dx = (k - 1) * 0.12
                if np.isfinite(sm[i, k]):
                    mem.add(Dot(ax.c2p(i + dx, math.log10(max(sm[i, k], 10))), radius=0.06, color=TR))
                if np.isfinite(st[i, k]):
                    gen.add(Dot(ax.c2p(i + dx, math.log10(st[i, k])), radius=0.08, color=TE))
                else:
                    never.add(MathTex(r"\times", font_size=30, color=C.SURPRISE).move_to(ax.c2p(i + dx, math.log10(cap))))
        lg = VGroup(label(r"grey: \ memorized \ ($99\%$ of the seen entries)", font_size=22, color=TR),
                    label(r"yellow: \ generalized \ ($95\%$ of the unseen)", font_size=22, color=TE),
                    label(r"red $\times$: \ not by the end", font_size=22, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lg.move_to([4.6, 1.4, 0])
        med = [float(np.nanmedian(r)) if np.isfinite(r).any() else float("nan") for r in st]
        ok = [i for i, v in enumerate(med) if np.isfinite(v)]
        faster = len(ok) >= 2 and med[ok[-1]] < med[ok[0]]
        n_never = int((~np.isfinite(st)).sum())
        tag = note(r"computed: \ five weight decays, \ three seeds each, \ the same data").to_corner(DL, buff=0.2)
        said2 = (
            f"The more weight decay, the sooner it comes: from step {med[ok[0]]:,.0f} at {wds[ok[0]]:g} to "
            f"{med[ok[-1]]:,.0f} at {wds[ok[-1]]:g}. " if faster else "Its timing varies with the weight decay. "
        )
        never_w = max((wds[i] for i in range(len(wds)) if (~np.isfinite(st[i])).any()), default=0.0)
        said3 = (
            f"And in {n_never} of the {st.size} runs, all at a weight decay of {never_w:g} or less, it never comes "
            f"within the {cap:,} steps." if n_never else ""
        )
        with self.voiceover(
            "Is weight decay really what drives it? Sweep it, from none to three, three seeds each. "
            f"<bookmark mark='a'/> Memorizing takes between {np.nanmin(sm):,.0f} and {np.nanmax(sm):,.0f} steps every "
            "time. "
            "<bookmark mark='b'/> Generalizing does not. "
            + said2
            + "<bookmark mark='c'/> "
            + said3
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(capl), FadeIn(capt), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in mem], lag_ratio=0.03), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in gen], lag_ratio=0.05), FadeIn(lg[1]))
            if len(never):
                self.play(FadeIn(never), FadeIn(lg[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        g = load("grok")
        P = int(g["P"])
        spec = np.asarray(g["spectrum"], float)  # snapshots x 48 frequencies
        steps = [int(v) for v in g["snap_steps"]]
        share = np.asarray(g["share5"], float)
        key = [int(k) for k in g["key_freqs"]]
        Wc = np.asarray(g["wd"])
        acc_at = [float(np.interp(s_, Wc[:, 0], Wc[:, 2])) for s_ in steps]
        nf = spec.shape[1]
        top = float(spec.max())
        base_y = -2.4
        bw = 0.1

        def bars_at(t):
            return VGroup(*[Rectangle(width=bw * 0.85, height=max(3.4 * v / top, 0.01), stroke_width=0,
                                      fill_color=C.BITS if (i + 1) in key and t == len(steps) - 1 else LAZY, fill_opacity=0.9)
                            .move_to([-6.0 + bw * i + bw / 2, base_y, 0], aligned_edge=DOWN) for i, v in enumerate(spec[t])])

        bars = bars_at(0)
        base = Line([-6.05, base_y, 0], [-6.0 + bw * nf + 0.05, base_y, 0], color=GREY_C, stroke_width=1.5)
        fl = label(rf"the number vectors' energy at each frequency, \ $1$ to ${nf}$", font_size=22, color=GREY_A)
        fl.next_to(base, DOWN, buff=0.15).align_to(base, LEFT)
        clock = VGroup(label(r"step", font_size=24, color=GREY_A), Integer(steps[0], font_size=28, color=C.BITS))
        clock.arrange(RIGHT, buff=0.2).move_to([-3.6, 2.6, 0])
        acc = VGroup(label(r"unseen entries right", font_size=22, color=GREY_A),
                     DecimalNumber(100 * acc_at[0], num_decimal_places=0, unit=r"\%", font_size=26, color=TE))
        acc.arrange(RIGHT, buff=0.2).next_to(clock, DOWN, buff=0.12)
        sh = VGroup(label(r"share in the top five", font_size=22, color=GREY_A),
                    DecimalNumber(100 * share[0], num_decimal_places=0, unit=r"\%", font_size=26, color=C.BITS))
        sh.arrange(RIGHT, buff=0.2).next_to(acc, DOWN, buff=0.12)
        # the numbers placed by the vectors' two main directions, through training
        snaps = np.asarray(g["snap_xy"], float)
        snaps = snaps / np.abs(snaps).max(axis=(1, 2), keepdims=True) * 2.2

        def place(Q):
            return [[3.6 + p_[0], -0.3 + p_[1], 0] for p_ in Q]

        pts = VGroup(*[Dot(q, radius=0.045, color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.MODEL_Q), i / P))
                       for i, q in enumerate(place(snaps[0]))])
        pl = label(r"the $97$ numbers, \ along their final two main directions", font_size=20, color=GREY_A)
        pl.move_to([3.6, 2.6, 0])
        idx = [0] + [i for i in range(1, len(steps)) if i % 2 == 0 or steps[i] <= 1000] + [len(steps) - 1]
        idx = sorted(set(idx))
        # the rise of the share relative to generalization
        t_te = int(g["t_test_wd"])
        i_te = int(np.searchsorted(steps, t_te))
        early = share[min(i_te, len(share) - 1) // 2] > share[0] + 0.5 * (share[-1] - share[0])
        said4 = (
            "Long before the unseen entries come right, a few frequencies start to grow, quietly: "
            if early else "As the unseen entries come right, a few frequencies take over: "
        )
        with self.voiceover(
            "What rule did it find? Look at the vectors it learned for the numbers, and ask which waves around the "
            "clock they contain: their Fourier spectrum. <bookmark mark='a'/> Watch it through training. At first "
            "the energy is spread over all frequencies, noise. "
            + said4
            + f"by the end, {100 * share[-1]:.0f} percent of the energy sits in five of the {nf}. "
            "<bookmark mark='b'/> And the numbers, seen along their main directions, settle onto circles."
        ) as vo:
            self.play(FadeIn(bars), Create(base), FadeIn(fl), FadeIn(clock), FadeIn(acc), FadeIn(sh), FadeIn(pts), FadeIn(pl))
            vo.wait_until("a")
            for t in idx[1:]:
                new = bars_at(t)
                self.play(Transform(bars, new), *[d.animate.move_to(q) for d, q in zip(pts, place(snaps[t]))],
                          clock[1].animate.set_value(steps[t]), acc[1].animate.set_value(100 * acc_at[t]),
                          sh[1].animate.set_value(100 * share[t]), run_time=0.22, rate_func=linear)
            vo.wait_until("b")
            kl = label(r"yellow: \ the five key frequencies, \ " + ", ".join(str(k) for k in key), font_size=22, color=C.BITS)
            kl.next_to(fl, UP, buff=0.05).align_to(fl, LEFT).shift(UP * 3.55)
            self.play(FadeIn(kl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circuit(self):
        g = load("grok")
        P = int(g["P"])
        key = [int(k) for k in g["key_freqs"]]
        circ = np.asarray(g["circles"], float)[0]
        circ = circ / np.abs(circ).max() * 1.15
        k0 = key[0]
        pts = VGroup(*[Dot([5.0 + p_[0], -1.25 + p_[1], 0], radius=0.045,
                           color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.MODEL_Q), i / P)) for i, p_ in enumerate(circ)])
        nums = VGroup(*[MathTex(str(i), font_size=16, color=GREY_A).next_to(pts[i], UR, buff=0.02) for i in (0, 1, 2)])
        cl = label(rf"each number $a$, \\ along $\cos$ and $\sin$ of frequency ${k0}$", font_size=20, color=GREY_A)
        cl.next_to(pts, DOWN, buff=0.25)
        colors = {r"\omega": C.BITS}
        rows = [
            cmath(r"a \mapsto", r"(\cos \omega a,\ \sin \omega a)", r",\quad \omega = 2\pi k / 97", font_size=32, colors=colors),
            cmath(r"\cos \omega(a+b)", r"=", r"\cos \omega a \cos \omega b - \sin \omega a \sin \omega b", font_size=32, colors=colors),
            cmath(r"\text{score}(c)", r"\approx", r"\textstyle\sum_k \cos \omega_k (a + b - c)", font_size=32, colors=colors),
        ]
        whys = [why(r"a number becomes an angle"), why(r"adding angles"), why(r"peaks at $c = a + b \bmod 97$")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-1.6, buff=0.45, edge=6.9)
        r2 = float(g["circuit_r2"])
        fit = label(rf"the trained network's scores, \ fitted by these five waves alone: \\ ${100 * r2:.0f}\%$ of their "
                    r"variation", font_size=24, color=C.BITS).to_edge(LEFT, buff=0.5).set_y(-1.0)
        kd, kds = np.asarray(g["kd"], float), np.asarray(g["kd_steps"], float)
        kdn = np.asarray(g["kd_nowd"], float)[:len(kds)]
        ytop = max(0.02, math.ceil(max(kd.max(), kdn.max()) * 1.1 * 50) / 50)
        ax = CornerAxes(x_range=[0, math.log10(kds.max()) + 0.1, 1], y_range=[0, ytop, ytop / 2], x_length=3.6, y_length=1.3,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -2.95, 0])
        kc = curve(ax, np.log10(kds), kd, RICH, 3)
        kcn = DashedVMobject(curve(ax, np.log10(kds), kdn, C.SURPRISE, 2.5), num_dashes=30)
        t_te = int(g["t_test_wd"])
        tm = DashedLine(ax.c2p(math.log10(t_te), 0), ax.c2p(math.log10(t_te), ytop), color=TE, stroke_width=1.5)
        kl = label(r"how far the tangent kernel has moved \\ (against log steps; \ yellow line: \ generalized)",
                   font_size=18, color=GREY_A)
        kl.next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
        ky = VGroup(MathTex(f"{ytop:.2f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, ytop), LEFT, buff=0.06),
                    MathTex("0", font_size=16, color=GREY_B).next_to(ax.c2p(0, 0), LEFT, buff=0.06))
        kg = VGroup(label(r"solid: \ weight decay $1$", font_size=18, color=RICH),
                    label(r"dashed: \ none", font_size=18, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        kg.next_to(ax, RIGHT, buff=0.15).align_to(ax, UP)
        i_te = int(np.searchsorted(kds, t_te))
        before = float(kd[max(0, min(i_te, len(kd)) // 3)])
        after = float(kd[-1])
        at_te = float(kd[min(i_te, len(kd) - 1)])
        moved_late = after > 2 * before and after > 0.1
        early = at_te > 0.6 * after
        nowd_far = kdn[-1] > 1.5 * after
        cite_ = cite(r"N.~Nanda et al.\ (2023); \ T.~Kumar, B.~Bordelon, S.~Gershman \& C.~Pehlevan (2023)", corner=DR)
        if moved_late:
            said5 = (
                f"Its tangent kernel barely moves while it memorizes, then travels far as it generalizes, to a "
                "distance "
                f"of {after:.2f}. Tanishq Kumar and colleagues argued in 2023 that grokking is exactly this: a network "
                "that first fits lazily, with its starting kernel, then slowly learns the features that generalize."
            )
        elif early and nowd_far:
            said5 = (
                f"Measure how far its tangent kernel moves: only to a distance of {after:.2f}, most of it before the "
                f"jump. Without weight decay it moves further, to {kdn[-1]:.2f}, and still never generalizes. Tanishq "
                "Kumar and colleagues argued in 2023 that grokking can be a slow move from lazy to rich training; in "
                "our network the kernel's movement alone does not mark the moment, and the weight decay does the work."
            )
        else:
            said5 = (
                f"Its tangent kernel moves steadily through training, to a distance of {after:.2f}. Tanishq Kumar and "
                "colleagues argued in 2023 that grokking can be a slow move from lazy to rich training, away from the "
                "starting kernel."
            )
        with self.voiceover(
            "Each number becomes a point on a circle, an angle. <bookmark mark='a'/> Adding two numbers on a clock "
            "is adding two angles, and the cosine of a sum is a sum of products of cosines and sines, which the ReLU "
            "units can build. <bookmark mark='b'/> The score of each answer c is then a sum of waves that peak where "
            f"c equals a plus b. Fit the trained network's scores with the five waves alone: they account for "
            f"{100 * r2:.0f} percent of the variation. Neel Nanda and colleagues worked this circuit out in 2023, "
            "one of the first complete explanations of what a trained network computes; part thirty takes the idea "
            "to real models. <bookmark mark='c'/> And chapter two's question returns: is this network lazy? "
            + said5
        ) as vo:
            self.play(FadeIn(pts), FadeIn(nums), FadeIn(cl), FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(fit))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(kl), FadeIn(ky), FadeIn(kg), Create(kc), Create(kcn), Create(tm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"With more weight decay, \ will understanding come sooner, \ later, \ or not at all? \ "
                          r"And with none?")
        with self.voiceover(
            "Pause and predict. With more weight decay, will understanding come sooner, later, or not at all? And "
            "with none?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Memorize first, \ understand later",
                           r"A network can fit its data long before it finds the rule; \ weight decay pushes it "
                           r"toward the rule, \ here a small trigonometric circuit.",
                           r"next: \ circuits inside real models, \ Part 30")
        with self.voiceover(
            "The takeaway: a network can fit its data long before it finds the rule, and weight decay pushes it "
            "toward the rule, which here is a small trigonometric circuit. Part thirty looks for circuits like it "
            "inside real models."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
