from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import DECAY, K, PART, Q, SSM_C, STATE, V, curve, load, sci


def bucket_picture() -> VGroup:
    """A state-space model as a leaky bucket: the input pours in, the level leaks slowly away, the level is read."""
    w_top, w_bot, h = 1.3, 1.0, 1.3
    wall = VMobject(color=GREY_A, stroke_width=3).set_points_as_corners(
        [[-w_top / 2, h / 2, 0], [-w_bot / 2, -h / 2, 0], [w_bot / 2, -h / 2, 0], [w_top / 2, h / 2, 0]])
    lvl = 0.15  # the water's top, in the bucket's coordinates
    f = (lvl + h / 2) / h
    w_lvl = w_bot + (w_top - w_bot) * f
    water = Polygon([-w_bot / 2, -h / 2, 0], [w_bot / 2, -h / 2, 0], [w_lvl / 2, lvl, 0], [-w_lvl / 2, lvl, 0],
                    stroke_width=0, fill_color=STATE, fill_opacity=0.7)
    pour = Arrow([-0.15, h / 2 + 0.7, 0], [-0.15, lvl + 0.05, 0], buff=0, color=K, stroke_width=4,
                 max_tip_length_to_length_ratio=0.15)
    pl = label(r"input $x$ pours in", font_size=20, color=K).next_to(pour, RIGHT, buff=0.12).shift(UP * 0.35)
    leak = Arrow([w_bot / 2 - 0.05, -h / 2 + 0.12, 0], [w_bot / 2 + 0.6, -h / 2 - 0.15, 0], buff=0, color=DECAY,
                 stroke_width=3, max_tip_length_to_length_ratio=0.25)
    ll = label(r"slowly leaks", font_size=20, color=DECAY).next_to(leak, RIGHT, buff=0.1)
    tick = DashedLine([-w_lvl / 2 - 0.35, lvl, 0], [-w_lvl / 2 - 0.05, lvl, 0], color=STATE, stroke_width=2)
    hl = label(r"the level $h$: \\ what you read", font_size=20, color=STATE).next_to(tick, LEFT, buff=0.1)
    return VGroup(water, wall, pour, pl, leak, ll, tick, hl)


class SSM(VoiceoverScene):
    def construct(self):
        self.card()
        self.continuous()
        self.zoh()
        self.hippo()
        self.s4()

    def card(self):
        card = chapter_card(8, r"State-space models", r"How should a continuous memory be read in steps?", part=PART)
        with self.voiceover("Chapter eight. State-space models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def continuous(self):
        s = load("ssm")
        t = np.asarray(s["t"], float)
        deltas = [float(v) for v in s["deltas"]]
        colors = {r"h": STATE, r"x": K, r"y": Q, r"\Delta": DECAY}
        f1 = cmath(r"h'(t)", "=", r"A\,", r"h", r"(t) + B\,", r"x", r"(t)", r",\qquad", r"y", r"(t) = C\,", r"h", r"(t)",
                   colors=colors, font_size=38).to_edge(UP, buff=0.4)
        f2 = cmath(r"h", r"_t", "=", r"e^{", r"\Delta", r"A}\,", r"h", r"_{t-1}", "+", r"\Delta", r"\,B\,", r"x", r"_t",
                   colors=colors, font_size=38).next_to(f1, DOWN, buff=0.35)
        f2l = label(r"read in steps of size $\Delta$", font_size=22, color=GREY_A).next_to(f2, RIGHT, buff=0.3)
        ax = Axes(x_range=[0, t[-1], 20], y_range=[0, 1.05, 0.5], x_length=7.4, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.6, -1.7, 0])
        xn = label(r"tokens since an input", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yn = label(r"how much of it the state still holds", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cols = [C.SURPRISE, C.BITS, C.INTERVAL]
        cs = VGroup(*[curve(ax, t, np.asarray(s[f"imp{dt:g}"]), c_, 3.5) for dt, c_ in zip(sorted(deltas, reverse=True), cols)])
        ks = VGroup(*[label(rf"$\Delta = {dt:g}$", font_size=24, color=c_) for dt, c_ in zip(sorted(deltas, reverse=True), cols)])
        ks.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, -1.4, 0])
        cite_ = cite(r"A.~Gu, K.~Goel \& C.~R\'e, \textit{S4} (2022)", corner=DR)
        # the equation at work: a leaky state, pushed by two pulses of input (A = -1, B = C = 1)
        tt = np.linspace(0, 10, 400)
        xin = ((tt > 1) & (tt < 1.6)).astype(float) + 0.7 * ((tt > 4.5) & (tt < 5.1))
        hh = np.zeros_like(tt)
        for i in range(1, len(tt)):
            hh[i] = hh[i - 1] + (tt[i] - tt[i - 1]) * (-hh[i - 1] + 1.6 * xin[i - 1])
        bx = Axes(x_range=[0, 10, 2], y_range=[0, 1.1, 0.5], x_length=8.0, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-0.6, -1.0, 0])
        kx = label(r"input $x(t)$", font_size=24, color=K)
        kh = label(r"state $h(t)$: \\ rises, then leaks away", font_size=24, color=STATE)
        bx.shift(LEFT * 0.8)
        VGroup(kx, kh).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bx, RIGHT, buff=0.4)
        keep_in_frame(VGroup(kx, kh))
        lx = VMobject(color=K, stroke_width=3).set_points_as_corners([bx.c2p(a_, b_) for a_, b_ in zip(tt, xin)])
        lh = VMobject(color=STATE, stroke_width=4).set_points_smoothly([bx.c2p(a_, b_) for a_, b_ in zip(tt[::4], hh[::4])])
        bl = note(r"illustrative: \ $A = -1$").next_to(bx, DOWN, buff=0.15).align_to(bx, LEFT)
        dot = glow_dot(bx.c2p(0, 0), color=STATE, radius=0.08)
        bucket = gloss(r"state-space model", r"a leaky bucket: input pours in, the level slowly \\ leaks away, "
                       r"and you read the level", bucket_picture(), width=4.6, color=STATE).to_corner(UR, buff=0.3)
        bucket.shift(DOWN * 1.0)
        with self.voiceover(
            "A different road to the same place started in control theory. A state-space model is a differential "
            "equation: a hidden state h that evolves, pushed by the input x, read out as y. <bookmark mark='l'/> "
            "Picture a leaky bucket: the input pours in, the level slowly leaks away, and the level is what you "
            "read. <bookmark mark='a'/> "
            "Read a text in steps of size delta, and it becomes a recurrence: shrink the state, add the input. "
            "<bookmark mark='b'/> The step size sets the memory. Small steps, and an input lingers for a long time; "
            "large steps, and it's gone in a few tokens."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_))
            vo.wait_until("l")
            self.play(FadeIn(bucket, shift=UP * 0.2))
            self.play(Create(bx), Create(lx), FadeIn(kx), FadeIn(bl), run_time=1.2)
            self.play(Create(lh), MoveAlongPath(dot, lh.copy()), FadeIn(kh), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeOut(bucket), Write(f2), FadeIn(f2l))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(bx, lx, lh, kx, kh, bl, dot)))
            self.play(Create(ax), FadeIn(xn), FadeIn(yn))
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.4), FadeIn(ks), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zoh(self):
        z = load("zoh")
        colors = {r"h": STATE, r"x": K, r"\Delta": DECAY, r"\bar A": SSM_C, r"\bar B": SSM_C}
        rows = [
            cmath(r"h(t+\Delta)", "=", r"e^{\Delta A} h(t) + \int_0^{\Delta} e^{(\Delta - s)A} B\, x(t+s)\, ds", font_size=32),
            cmath(r"h(t+\Delta)", "=", r"e^{\Delta A} h(t) + \Big(\int_0^{\Delta} e^{uA}\, du\Big) B\, x_t", font_size=32),
            cmath(r"h(t+\Delta)", "=", r"e^{\Delta A} h(t) + A^{-1}\big(e^{\Delta A} - I\big) B\, x_t", font_size=32),
            cmath(r"h_t", "=", r"\bar A\, h_{t-1} + \bar B\, x_t", colors=colors, font_size=34),
        ]
        whys = [why(r"solve the linear ODE \ (variation of constants)"), why(r"hold the input still over the step: \ $u = \Delta - s$"),
                why(r"$\int e^{uA} du = A^{-1} e^{uA}$"), why(r"the zero-order hold: \ $\bar A = e^{\Delta A}$, \ "
                                                                   r"$\bar B = A^{-1}(e^{\Delta A} - I) B$")]
        deltas = np.asarray(z["deltas"], float)
        g = axes([math.log10(deltas.min()) - 0.1, math.log10(deltas.max()) + 0.1], [-15.5, 3], x_length=4.6, y_length=3.0,
                 xlabel=r"step $\Delta$", ylabel=r"largest error \ (relative)", xticks=[math.log10(0.025), math.log10(0.1), math.log10(0.4)],
                 yticks=[-15, -10, -5, 0], xfmt=lambda v: f"{10 ** v:.3g}", yfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[3.9, -1.65, 0], font_size=17)
        ax = g.ax
        cols = {"euler": C.SURPRISE, "bilinear": C.BITS, "zoh": C.INTERVAL}
        names = {"euler": r"Euler: \ $\bar A = I + \Delta A$", "bilinear": r"bilinear", "zoh": r"zero-order hold"}
        lines = VGroup(*[curve(ax, np.log10(deltas), np.log10(np.clip(np.asarray(z[f"err_{k}"]), 1e-16, 1e3)), c_, 3)
                         for k, c_ in cols.items()])
        leg = legend([(cols[k], names[k]) for k in cols], font_size=16).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        ee = np.asarray(z["err_euler"])
        tag = note(r"a damped oscillator, $2$ numbers of state, \ against a fine Runge--Kutta solution", font_size=16)
        tag.next_to(g, DOWN, buff=0.1)
        unstable = ee[0] > 1
        zm, ze = f"{float(np.max(z['err_zoh'])):.0e}".split("e")
        ze = -int(ze)
        v = (f"Euler's simple step is not just less accurate: at the largest step it is unstable, and the error grows "
             f"to {ee[0]:.0f} times the signal. " if unstable else "")
        with self.voiceover(
            "How should a continuous memory be read in steps? Solve the equation exactly over one step: the state "
            "decays by the exponential of delta A, plus the input, accumulated with the same decay. "
            "<bookmark mark='a'/> If the input is held constant over the step, the integral can be done. "
            "<bookmark mark='b'/> It comes out as A inverse times e to the delta A, minus the identity, times B. "
            "<bookmark mark='c'/> That's the zero-order hold: a recurrence with A bar and B bar that is exact for "
            "such inputs. <bookmark mark='d'/> We checked it on a small oscillator: the zero-order hold matches a fine "
            f"numerical solution to within {zm} times ten to the minus {ze}. The bilinear rule's error "
            f"shrinks with the square of the step, its measured slope {float(z['slope_bilinear']):.1f}. " + v
            + "S4 used the bilinear rule; Mamba uses the zero-order hold for A."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.6, buff=0.32, edge=6.8)
            step(0)
            for k, m in enumerate("abc", start=1):
                vo.wait_until(m)
                step(k)
            vo.wait_until("d")
            self.play(FadeIn(g), FadeIn(leg), FadeIn(tag))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hippo(self):
        h = load("hippo")
        f = np.asarray(h["f"])
        L = int(h["L"])
        at = [int(a) for a in h["snaps_at"]]
        Ns = [int(n) for n in h["Ns"]]

        def snaps(N):
            flat = np.asarray(h[f"snaps_{N}"])
            out, i = [], 0
            for a in at:
                out.append(flat[i:i + a])
                i += a
            return out

        s8, s32 = snaps(8), snaps(32)
        g = axes([0, L], [-1.15, 1.15], x_length=8.0, y_length=3.0, xlabel=r"time", ylabel=r"the signal, \ and what the memory holds",
                 center=[-1.9, 0.9, 0])
        ax = g.ax
        sig = curve(ax, np.arange(L), f, GREY_B, 2)

        def recs(k):
            xs = np.linspace(0, at[k] - 1, at[k])
            return VGroup(curve(ax, xs[::4], s8[k][::4], C.SURPRISE, 3), curve(ax, xs[::4], s32[k][::4], C.INTERVAL, 3))

        cur = recs(0)
        cursor = DashedLine(ax.c2p(at[0], -1.15), ax.c2p(at[0], 1.15), color=WHITE, stroke_width=1.5)
        leg = legend([(GREY_B, r"the signal"), (C.SURPRISE, r"$N = 8$ numbers"), (C.INTERVAL, r"$N = 32$ numbers")],
                     font_size=18).move_to([4.9, 1.2, 0])
        colors = {r"c": SSM_C, r"f": K}
        fe = cmath(r"\tfrac{d}{dt} c(t)", "=", r"-\tfrac{1}{t} A\, c(t) + \tfrac{1}{t} B\, f(t)", colors=colors, font_size=32)
        fe.move_to([-2.4, -1.35, 0])
        fl = label(r"$c(t)$: \ the coefficients of the best polynomial fit \ to all of $f$ up to $t$ \ (Legendre polynomials, "
                   r"\ equal weight on the whole past)", font_size=18, color=GREY_A).next_to(fe, DOWN, buff=0.15)
        bars = VGroup()
        for i, N in enumerate(Ns):
            e, b = float(h[f"err_{N}"]), float(h[f"best_{N}"])
            bars.add(label(rf"$N = {N}$: \ ${e:.3f}$ \ (best fit ${b:.3f}$)", font_size=18,
                           color=C.INTERVAL if abs(e - b) < 0.01 else GREY_A))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, -1.7, 0])
        bh = label(r"error at the end, \ relative", font_size=18, color=GREY_A).next_to(bars, UP, buff=0.12).align_to(bars, LEFT)
        cite_ = cite(r"A.~Gu, T.~Dao, S.~Ermon, A.~Rudra \& C.~R\'e, \textit{HiPPO} (2020)", corner=UL, font_size=17)
        close = [N for N in Ns if abs(float(h[f"err_{N}"]) - float(h[f"best_{N}"])) < 0.01]
        with self.voiceover(
            "But which A? Albert Gu and colleagues asked what it would mean for a state to remember a whole signal. "
            "Their answer, HiPPO, in 2020: keep the coefficients of the best polynomial fit to everything seen so "
            "far. <bookmark mark='a'/> That fit can be updated as each sample arrives, by an equation of exactly this "
            "form, with a particular matrix A. <bookmark mark='b'/> Here it is memorizing a signal online, one sample "
            f"at a time, {L:,} of them, with eight numbers and with thirty-two. <bookmark mark='c'/> At any moment, the "
            "memory can be unpacked into its picture of the whole past: coarse with eight numbers, close with "
            f"thirty-two. <bookmark mark='d'/> For {len(close)} of the {len(Ns)} sizes, the error at the end is within "
            "a hundredth of the best possible polynomial fit, which the memory never stored: the recurrence keeps it "
            "up to date."
        ) as vo:
            self.play(FadeIn(g), Create(sig), FadeIn(cite_), FadeIn(leg))
            vo.wait_until("a")
            self.play(Write(fe), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(cursor), Create(cur))
            vo.wait_until("c")
            for k in range(1, len(at)):
                nc = recs(k)
                self.play(Transform(cur, nc), cursor.animate.move_to(ax.c2p(at[k] - 1, 0)), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def s4(self):
        z = load("zoh")
        Kk = np.asarray(z["kernel"])
        n = len(Kk)
        top = float(np.abs(Kk).max()) * 1.1
        g = axes([0, n], [-top, top], x_length=7.2, y_length=2.6, xlabel=r"lag $j$ \ (steps back)",
                 ylabel=r"the kernel: \ $K_j = C \bar A^{j} \bar B$", center=[-2.2, 0.7, 0])
        ax = g.ax
        stems = VGroup(*[Line(ax.c2p(j, 0), ax.c2p(j, Kk[j]), color=SSM_C, stroke_width=2) for j in range(n)])
        colors = {r"K": SSM_C, r"x": K, r"y": Q}
        f = cmath(r"y_t", "=", r"\sum_{j \ge 0}", r"K_j", r"\, x_{t-j}", colors=colors, font_size=36).move_to([-2.2, -1.5, 0])
        fl = label(r"the same SSM as one long convolution: \ trained in parallel, \ with the FFT", font_size=20,
                   color=GREY_A).next_to(f, DOWN, buff=0.15)
        chk = label(rf"recurrence vs convolution, \ ${n}$ steps: \ ${sci(float(z['conv_diff']))}$", font_size=20,
                    color=C.INTERVAL).move_to([4.4, 0.7, 0])
        hc = history_card(2021, r"S4", r"Gu, Goel \& R\'e: \ HiPPO's matrix, \ a structured $A$ (diagonal plus low "
                          r"rank), \ and the convolution view; \ the first model to solve Path-X, \ $16{,}384$ steps long",
                          color=SSM_C, width=4.8, font_size=19).move_to([4.4, -1.6, 0])
        with self.voiceover(
            "A state-space model with a fixed A and B has one more face. Unroll the recurrence, and each output is a "
            "weighted sum of past inputs, with weights C times A bar to the j, times B bar: <bookmark mark='a'/> a "
            "convolution, with a kernel as long as the text. <bookmark mark='b'/> We checked that both give the "
            "same outputs. A convolution can be trained on a whole sequence at once with the fast Fourier "
            "transform. <bookmark mark='c'/> That was S4, by Gu, Karan Goel and Christopher Ré, in 2021: HiPPO's "
            "matrix, made fast by a clever structure. It was the first model to solve Path-X, a test that asks "
            "whether two dots in a sixteen-thousand-pixel image are connected, read one pixel at a time. "
            "<bookmark mark='d'/> But its kernel is the same for every input: an S4 layer cannot decide, from what "
            "it reads, what to keep."
        ) as vo:
            self.play(FadeIn(g))
            self.play(LaggedStart(*[Create(s_) for s_ in stems], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(chk))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(stems, color=WHITE, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()
