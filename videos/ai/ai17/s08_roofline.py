from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (A_C, B_C, BYTEC, CPUC, FLOPC, GPUC, PART, gbs, gflops, load, loglog, pow10,
                                   roof_line)
from videos.ai.ai17.specs import GPUS, TPU1


class Roofline(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.ours()
        self.climb()
        self.gpus()

    def card(self):
        card = chapter_card(7, r"The roofline", r"Is a program limited by arithmetic or by memory?", part=PART)
        with self.voiceover("Chapter seven. The roofline."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"W": FLOPC, r"P": FLOPC, r"Q": BYTEC, r"\beta": BYTEC, r"I": FLOPC, r"T": WHITE}
        rows = [
            cmath(r"T", r"\ge", r"\frac{W}{P}", colors=colors, font_size=40),
            cmath(r"T", r"\ge", r"\frac{Q}{\beta}", colors=colors, font_size=40),
            cmath(r"\frac{W}{T}", r"\le", r"\min\Big(P,\ \beta\,\frac{W}{Q}\Big)", colors=colors, font_size=40),
            cmath(r"\text{speed}", r"\le", r"\min(P,\ \beta I)", colors=colors, font_size=40),
        ]
        whys = [why(r"$W$ operations at peak speed $P$"), why(r"$Q$ bytes at bandwidth $\beta$"),
                why(r"both at once: \ divide $W$ by $T$"), why(r"$I = W/Q$, \ the arithmetic intensity")]
        step = ladder(self, rows, whys, keep=4, top=3.25, x=-2.2, buff=0.32, edge=6.8)
        hc = history_card(2009, r"Samuel Williams, Andrew Waterman \& David Patterson, \ Berkeley",
                          r"\textit{Roofline}: \ one picture of what bounds a program on a machine", width=6.0,
                          color=FLOPC, font_size=20).to_corner(DL, buff=0.3)
        # the picture the inequalities draw, built alongside them (schematic)
        g = axes([0, 4], [0, 3], x_length=4.6, y_length=2.4, xlabel=r"intensity $I$ (log)", ylabel=r"speed (log)",
                 center=[3.9, -2.2, 0], font_size=18)
        ax = g.ax
        roof = DashedLine(ax.c2p(0, 2.4), ax.c2p(4, 2.4), color=FLOPC, dash_length=0.08)
        rl = MathTex(r"P", font_size=26, color=FLOPC).next_to(ax.c2p(4, 2.4), RIGHT, buff=0.1)
        slope = DashedLine(ax.c2p(0, 0.2), ax.c2p(2.6, 3.0), color=BYTEC, dash_length=0.08)
        sl = MathTex(r"\beta I", font_size=26, color=BYTEC).next_to(ax.c2p(2.6, 3.0), LEFT, buff=0.1)
        xr = (2.4 - 0.2) / (2.8 / 2.6)
        best = VMobject(color=WHITE, stroke_width=4).set_points_as_corners([ax.c2p(0, 0.2), ax.c2p(xr, 2.4),
                                                                          ax.c2p(4, 2.4)])
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "Chapters two to six give a program two ways to be slow. <bookmark mark='a'/> If it does W operations "
            "on a machine whose peak is P operations a second, it takes at least W over P. <bookmark mark='b'/> If "
            "it moves Q bytes through a memory of bandwidth beta, it takes at least Q over beta. "
            "<bookmark mark='c'/> It can't beat either, so its speed, W over T, is at most the smaller of P and beta "
            "times W over Q. <bookmark mark='d'/> W over Q is the arithmetic intensity, I: operations per byte. "
            "So the speed is at most the minimum of P and beta times I. In 2009 Samuel Williams, Andrew Waterman "
            "and David Patterson at Berkeley drew this as a picture, and called it the roofline."
        ) as vo:
            step(0)
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(roof), FadeIn(rl))
            vo.wait_until("b")
            step(1)
            self.play(Create(slope), FadeIn(sl))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(Create(best), run_time=1.5)
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def machine_roof(self):
        mm, h = load("matmul"), load("hierarchy")
        P = max(r[1] for r in mm["np_float32"])
        B = max([float(v) for v in h["stream"].values()] + [float(mm["np_copy"][0])])  # the best streaming rate
        return mm, h, P, B

    def ours(self):
        mm, h, P, B = self.machine_roof()
        xr, yr = (-2, 3.3), (-1, 2.6)  # FLOP per byte; GFLOP/s
        g = loglog(xr, yr, x_length=8.0, y_length=4.8, xlabel=r"arithmetic intensity \ (FLOPs per byte)",
                   ylabel=r"GFLOP/s, \ one core of this computer", center=[-1.6, -0.3, 0])
        ax = g.ax
        roof = roof_line(ax, P / 1e9, B / 1e9, xr, color=WHITE, y_min=yr[0])
        ridge = math.log10(P / B)
        rl = DashedLine(ax.c2p(ridge, yr[0]), ax.c2p(ridge, math.log10(P / 1e9)), color=GREY_B, dash_length=0.08)
        rlab = label(rf"ridge: \ ${P / B:.1f}$", font_size=20, color=GREY_B)
        rlab.next_to(ax.c2p(ridge, (yr[0] + math.log10(P / 1e9)) / 2), RIGHT, buff=0.12)
        slope_l = label(rf"memory: \ ${gbs(B)}$ GB/s", font_size=22, color=BYTEC)
        slope_l.move_to(ax.c2p(-1.2, math.log10(B / 1e9 * 10 ** -1.2) + 0.55)).rotate(math.atan2(
            ax.c2p(1, 1)[1] - ax.c2p(0, 0)[1], ax.c2p(1, 1)[0] - ax.c2p(0, 0)[0]))
        roof_l = label(rf"arithmetic: \ ${gflops(P)}$ GFLOP/s", font_size=22, color=FLOPC)
        roof_l.next_to(ax.c2p(2.3, math.log10(P / 1e9)), UP, buff=0.12)

        def dot(I, perf, col, r=0.07):
            return Dot(ax.c2p(math.log10(I), math.log10(perf / 1e9)), radius=r, color=col)

        tb = float(h["stream"].get("triad", B))
        tri = dot(2 / 12, tb * 2 / 12, BYTEC)
        trl = label(r"STREAM triad", font_size=18, color=BYTEC).next_to(tri, DOWN, buff=0.1)
        gv = [(n, best) for n, best, _ in mm["gemv"] if 4 * n * n >= 32 * 2 ** 20]  # matrices far bigger than cache
        gemv = VGroup(*[dot(2 * n * n / (4 * n * n + 8 * n), b, A_C, 0.06) for n, b in gv])
        gl = label(r"matrix $\times$ vector", font_size=18, color=A_C).next_to(gemv[-1], DOWN, buff=0.12)
        mats = [(n, best) for n, best, _ in mm["np_float32"]]
        md = VGroup(*[dot(n / 6, b, B_C, 0.06) for n, b in mats])
        ml = VGroup(*[label(rf"${int(n)}$", font_size=15, color=B_C).next_to(d_, UP, buff=0.06)
                      for (n, _), d_ in zip(mats, md)])
        mlab = label(r"matrix $\times$ matrix, \ by size $n$", font_size=18, color=B_C)
        mlab.next_to(md[-1], RIGHT, buff=0.15).shift(DOWN * 0.3)
        pos = ValueTracker(0)
        pts = [d_.get_center() for d_ in md]

        def mover():
            v = pos.get_value()
            i = min(int(v), len(pts) - 2)
            f = v - i
            return glow_dot(pts[i] * (1 - f) + pts[i + 1] * f, color=FLOPC, radius=0.08)

        mv = always_redraw(mover)
        tag = note(rf"computed: \ fp32, \ one thread; \ load average ${mm['loadavg_before'][0]:.0f}$ on "
                   rf"${load('machine')['cores']}$ cores").to_corner(DR, buff=0.2)
        n_small, small = mats[0]
        n_big, big = max(mats, key=lambda t: t[1])
        gv_best = max(b for _, b in gv)
        with self.voiceover(
            "Here is the roofline of one core of this computer, measured. <bookmark mark='a'/> The sloped part: the "
            f"memory bandwidth, {gbs(B)} gigabytes a second, the fastest we measured one core stream through main "
            "memory. A program on the slope is waiting for memory; the classic test, STREAM's triad, sits on or "
            "under it. <bookmark mark='b'/> The flat part: the fastest "
            f"arithmetic we measured, {gflops(P)} billion operations a second. They meet at the ridge, "
            f"{P / B:.1f} operations per byte. <bookmark mark='c'/> A matrix times a vector does two operations "
            "per four-byte weight, and every weight is used once: it can't leave the slope. We measured at most "
            f"{gflops(gv_best)} billion a second. <bookmark mark='d'/> A matrix times a matrix has intensity n over "
            f"six. Watch it climb as n grows: at n of {int(n_small)}, overheads dominate and it manages "
            f"{gflops(small)}; by {int(n_big)}, it reaches {gflops(big)}, the roof."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(roof), run_time=1.5)
            self.play(FadeIn(slope_l), FadeIn(tri), FadeIn(trl))
            vo.wait_until("b")
            self.play(FadeIn(roof_l), Create(rl), FadeIn(rlab))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in gemv], lag_ratio=0.2), FadeIn(gl))
            vo.wait_until("d")
            self.add(mv)
            self.play(FadeIn(mlab))
            for k in range(1, len(pts)):
                self.play(pos.animate.set_value(k), FadeIn(md[k - 1]), FadeIn(ml[k - 1]), run_time=0.5)
            self.play(FadeIn(md[-1]), FadeIn(ml[-1]))
        mv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climb(self):
        mm, h, P, B = self.machine_roof()
        r = load("blocking")
        xr, yr = (-2, 3.3), (-1, 2.6)
        g = loglog(xr, yr, x_length=8.0, y_length=4.8, xlabel=r"arithmetic intensity \ (FLOPs per byte)",
                   ylabel=r"GFLOP/s, \ one core of this computer", center=[-1.6, -0.3, 0])
        ax = g.ax
        roof = roof_line(ax, P / 1e9, B / 1e9, xr, color=WHITE, y_min=yr[0])
        n = int(r["n"])
        I = math.log10(n / 6)
        blk = np.asarray(r["blocked"])
        steps = [(r["naive"], r"textbook loop", C.SURPRISE), (r["ikj"], r"loops reordered", B_C),
                 (float(blk.max()), r"tiled", FLOPC), (r["blas"], r"BLAS", CPUC)]
        dots = VGroup(*[Dot(ax.c2p(I, math.log10(v / 1e9)), radius=0.08, color=c_) for v, _, c_ in steps])
        labs = VGroup(*[label(rf"{t}: \ ${gflops(v)}$", font_size=20, color=c_).next_to(d_, RIGHT, buff=0.15)
                        for (v, t, c_), d_ in zip(steps, dots)])
        labs[3].shift(DOWN * 0.3)
        col = DashedLine(ax.c2p(I, yr[0]), ax.c2p(I, math.log10(P / 1e9)), color=GREY_C, dash_length=0.06)
        cl = label(rf"$n = {n:,}$: \ $I = n/6 \approx {n / 6:.0f}$".replace(",", "{,}"), font_size=20,
                   color=GREY_B).next_to(ax.c2p(I, yr[0] + 0.5), LEFT, buff=0.15)
        gap = r["blas"] / r["naive"]
        note_ = label(r"the roof is a ceiling, \\ not a promise", font_size=26, color=WHITE).move_to([4.9, -1.6, 0])
        mt = load("matmul_mt")
        Pn = max(x[1] for x in mt["np_float32"])
        ratio = Pn / P
        if ratio >= 1.5:
            many = (f"With all {int(mt['threads'])} cores the roof rises to {gflops(Pn)}, {ratio:.1f} times one "
                    "core; memory is shared, so the slope rises less.")
        else:
            many = (f"We also tried all {int(mt['threads'])} cores at once, but other jobs were using them, and the "
                    f"best we saw was {gflops(Pn)}: on a shared machine the roof you get is the roof you're left.")
        with self.voiceover(
            "Intensity is a property of the algorithm, but it only counts if the code earns it. "
            f"<bookmark mark='a'/> All four matrix products of chapter five have the same intensity on paper, n over "
            f"six, about {n / 6:.0f} operations per byte. <bookmark mark='b'/> The textbook loop sits far below "
            "the roof, because it fetches its numbers over and over: its real intensity is far lower. "
            "<bookmark mark='c'/> Reordering and tiling climb towards the roof, <bookmark mark='d'/> and the "
            f"library reaches it: {gap:.0f} times higher, on the same line. The roofline says what's possible; "
            "the gap below it is the kernel writer's job. " + many
        ) as vo:
            self.play(FadeIn(g), FadeIn(roof), Create(col), FadeIn(cl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(dots[0], scale=0.5), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(TransformFromCopy(dots[0], dots[1]), FadeIn(labs[1]))
            self.play(TransformFromCopy(dots[1], dots[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(TransformFromCopy(dots[2], dots[3]), FadeIn(labs[3]))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpus(self):
        mm, h, P, B = self.machine_roof()
        H = GPUS["H100"]
        xr, yr = (-2, 4), (-1, 6.3)
        g = loglog(xr, yr, x_length=8.4, y_length=5.0, xlabel=r"arithmetic intensity \ (FLOPs per byte)",
                   ylabel=r"GFLOP/s", center=[-1.4, -0.3, 0])
        ax = g.ax
        ours = roof_line(ax, P / 1e9, B / 1e9, xr, color=CPUC, y_min=yr[0])
        hroof = roof_line(ax, H["tensor"] / 1e9, H["bw"] / 1e9, xr, color=GPUC, y_min=yr[0])
        ridge = H["tensor"] / H["bw"]
        rl = DashedLine(ax.c2p(math.log10(ridge), yr[0]), ax.c2p(math.log10(ridge), math.log10(H["tensor"] / 1e9)),
                        color=GPUC, dash_length=0.08)
        lab_o = label(r"this computer, one core", font_size=20, color=CPUC).next_to(ax.c2p(2.0, math.log10(P / 1e9)),
                                                                                  UP, buff=0.1)
        lab_h = label(rf"H100: \ ${H['tensor'] / 1e12:.0f}$ TFLOP/s (BF16), \ ${H['bw'] / 1e12:.2f}$ TB/s",
                      font_size=20, color=GPUC).next_to(ax.c2p(1.5, math.log10(H["tensor"] / 1e9)), UP, buff=0.1)
        rlab = label(rf"ridge $\approx {ridge:.0f}$", font_size=20, color=GPUC)
        rlab.next_to(ax.c2p(math.log10(ridge), 2.0), RIGHT, buff=0.12)
        n_star = 3 * ridge  # BF16: I = 2n^3 / (3 n^2 * 2 bytes) = n/3
        dec = glow_dot(ax.c2p(0, math.log10(H["bw"] / 1e9)), color=C.SURPRISE, radius=0.09)
        decl = label(rf"one token at a time: \ $\approx 1$ FLOP/byte, \ ${100 * H['bw'] / H['tensor']:.1f}\%$ of peak",
                     font_size=20, color=C.SURPRISE).next_to(dec, DR, buff=0.15).shift(DOWN * 0.35)
        others = VGroup(label(rf"ridge points: \ TPU v1 ${TPU1['ridge']:,}$; \ K80 ${TPU1['ridge_k80']}$; \ "
                              rf"Haswell CPU ${TPU1['ridge_haswell']}$".replace(",", "{,}"), font_size=20,
                              color=GREY_A),
                        label(r"(Jouppi et al.\ 2017, \ operations per byte of weights)", font_size=18,
                              color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now put a GPU on the same axes. <bookmark mark='a'/> Our core's roofline is down in the corner. "
            f"<bookmark mark='b'/> An H100's tensor cores do about {H['tensor'] / 1e12:.0f} trillion operations a "
            f"second in 16-bit arithmetic, and its memory moves {H['bw'] / 1e12:.2f} terabytes a second. Its ridge "
            f"is at about {ridge:.0f} operations per byte. In 16-bit numbers, a square matrix product reaches it "
            f"once n is about {round(n_star, -1):.0f}. <bookmark mark='c'/> Now the problem that Part 19 is about. "
            "A language model writing one token at a time multiplies every weight once: about one operation per "
            f"byte. That's down on the slope, at {100 * H['bw'] / H['tensor']:.1f} percent of the peak. "
            "<bookmark mark='d'/> Google's TPU paper of 2017 used exactly this picture. Their chip's ridge was at "
            "1,350 operations per byte, a K80 GPU's at 9. Whether a chip is fast depends on where your program "
            "sits."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ours), FadeIn(lab_o))
            vo.wait_until("b")
            self.play(Create(hroof), FadeIn(lab_h), run_time=2.0)
            self.play(Create(rl), FadeIn(rlab))
            vo.wait_until("c")
            self.play(FadeIn(dec, scale=0.5), FadeIn(decl))
            vo.wait_until("d")
            self.play(FadeIn(others))
        self.wait(0.3)
        self.clear_scene()
